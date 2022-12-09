import React, { useCallback } from "react";
import Button from "react-bootstrap/Button";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Spinner from "react-bootstrap/Spinner";
import Tooltip from "react-bootstrap/Tooltip";

interface ButtonCardProps {
  isLoading: boolean;
  tooltipText: string;
  onClick: () => void;
  children: React.ReactNode;
}

export const ButtonCard: React.FunctionComponent<ButtonCardProps> = ({
  isLoading,
  tooltipText,
  onClick,
  children,
}) => {
  const renderTooltip = useCallback(
    (props: any) => (
      <Tooltip id="card-tooltip" {...props}>
        {tooltipText}
      </Tooltip>
    ),
    [tooltipText]
  );

  return (
    <OverlayTrigger
      placement="right"
      delay={{ show: 250, hide: 0 }}
      overlay={renderTooltip}
    >
      <Button
        className="text-card"
        disabled={isLoading}
        onClick={!isLoading ? () => onClick() : undefined}
        bsPrefix="no-css"
      >
        {!isLoading ? (
          children
        ) : (
          <span className="spinner-container">
            <Spinner
              className="initializing-spinner"
              animation="border"
              role="status"
            />
          </span>
        )}
      </Button>
    </OverlayTrigger>
  );
};
