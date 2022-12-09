from __future__ import annotations

import dataclasses
import re
from collections import Counter, defaultdict
from typing import Dict, Iterable, Mapping, Set, Tuple

import cleanco
import pylcs

SHARED_PREFIX_LENGTH_SIMILARITY_PRECONDITION = 3
CLEANCO_COMPANY_TERMS = cleanco.prepare_default_terms() + [
    (1, ["holding"]),
    (1, ["holdings"]),
]
CITY_COUNTY_SIMILARITY_THRESHOLD = 0.91
COMPANY_SIMILARITY_THRESHOLD = 0.82


@dataclasses.dataclass
class CompanyAggregator:
    """
    Helper class for cleansing large sets of company names

    There are two steps for cleaning company names:

        1) Simplify each individual name as much as possible.
            a) Remove parenthesized and bracketed text
            b) Use the `cleanco` Python package to remove
               filler names like "Corp", "Company",
               "Holdings", etc.
            c) Ignore capitalization, punctuation, whitespace

        2) Use a string distance metric to map similar company
           names to the same final name. This ensures equalities like:

           - "Father and Sons" ~= "Father&Sons"
           - "My Company" ~= "My Company USA"
           - "City of Houston, TX" ~= "City of Houston, Texas"
           - Many, many typos

           The LCS (Longest Common Subsequence) distance (normalized
           by total length) is used rather than the Levenshtein
           distance, so as to bias towards examples like

           - "My Company" ~= "My Company With More Text"

           and away from examples like

           - "ABC Energy Company" != "XYZ Energy Company"

           Lastly, we bucketize names by their first 3 letters
           before computing similarity. This drastically improves
           runtime efficiency and ensures no non-examples like
           the one immediately above.
    """

    prefix_aggregators: Dict[str, CompanySharedPrefixAggregator] = dataclasses.field(
        default_factory=lambda: defaultdict(CompanySharedPrefixAggregator)
    )

    @staticmethod
    def of(companies: Mapping[int, str]) -> CompanyAggregator:
        output = CompanyAggregator()
        for index, company in companies.items():
            output.add(index, company)
        return output

    @staticmethod
    def cleanse(name: str) -> str:
        # Remove:
        #  - parenthesized text
        #  - bracketed text
        #  - commas and periods
        name = re.sub(r"(\([^\(\)]*(\)|$))|(\[[^\[\]]*(\]|$))|,|\.", "", name)

        # Remove keywords like "company", "co", "holdings", "llc", etc.
        name = cleanco.clean.custom_basename(
            name, CLEANCO_COMPANY_TERMS, suffix=True, middle=True
        )

        # Remove whitespace and capitalize
        return re.sub(r"\s+", "", name).upper()

    def add(self, index: int, name: str):
        if not isinstance(name, str):
            return
        clean_name = CompanyAggregator.cleanse(name)
        prefix = clean_name[:SHARED_PREFIX_LENGTH_SIMILARITY_PRECONDITION]
        self.prefix_aggregators[prefix].add(index, name, clean_name)

    def aggregate(self) -> Dict[int, str]:
        output = dict()
        for prefix, prefix_aggregator in self.prefix_aggregators.items():
            merge_similar = len(prefix) == SHARED_PREFIX_LENGTH_SIMILARITY_PRECONDITION
            output.update(prefix_aggregator.aggregate(merge_similar=merge_similar))
        return output


@dataclasses.dataclass
class CompanySharedPrefixAggregator:
    clean_names: Dict[str, CompanyCleanseResult] = dataclasses.field(
        default_factory=lambda: defaultdict(CompanyCleanseResult)
    )

    @classmethod
    def lcs_similarity_score(cls, a: str, b: str):
        return 2 * pylcs.lcs_sequence_length(a, b) / (len(a) + len(b))

    @classmethod
    def are_similar(cls, a: str, b: str):
        score = CompanySharedPrefixAggregator.lcs_similarity_score(a, b)
        if ("CITY" in a and "CITY" in b) or ("COUNTY" in a and "COUNTY" in b):
            return score >= CITY_COUNTY_SIMILARITY_THRESHOLD
        else:
            return score >= COMPANY_SIMILARITY_THRESHOLD

    def add(self, index: int, dirty_name: str, clean_name: str):
        self.clean_names[clean_name].matching_indices.add(index)
        self.clean_names[clean_name].matching_names[dirty_name] += 1

    def aggregate(self, merge_similar=True) -> Dict[int, str]:
        if merge_similar:
            buckets: Dict[Tuple[str, ...], CompanyCleanseResult] = dict()
            for clean_name, cleanse_result in self.clean_names.items():
                names_to_merge = [clean_name]
                results_to_merge = [cleanse_result]
                for bucket_names, bucket_result in list(buckets.items()):
                    if any(
                        self.are_similar(clean_name, bucket_name)
                        for bucket_name in bucket_names
                    ):
                        names_to_merge.extend(bucket_names)
                        results_to_merge.append(bucket_result)
                        buckets.pop(bucket_names)
                names_to_merge.sort()
                buckets[tuple(names_to_merge)] = CompanyCleanseResult.merge(
                    results_to_merge
                )
            results = buckets.values()
        else:
            results = self.clean_names.values()

        output = dict()
        for result in results:
            output.update(dict.fromkeys(result.matching_indices, result.canonical_name))
        return output


@dataclasses.dataclass
class CompanyCleanseResult:
    matching_indices: Set[int] = dataclasses.field(default_factory=set)
    matching_names: Counter = dataclasses.field(default_factory=Counter)

    @property
    def canonical_name(self):
        names_by_frequency = self.matching_names.most_common()
        for name, _ in names_by_frequency:
            # Use most common non-uppercase name if it exists
            if not name.isupper():
                return name
        # Otherwise, use most common name
        return names_by_frequency[0][0]

    @staticmethod
    def merge(results: Iterable[CompanyCleanseResult]) -> CompanyCleanseResult:
        merged = CompanyCleanseResult()
        for result in results:
            merged.matching_names.update(result.matching_names)
            merged.matching_indices.update(result.matching_indices)
        return merged
