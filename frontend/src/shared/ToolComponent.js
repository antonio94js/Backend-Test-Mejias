import React from 'react';
import { UncontrolledTooltip } from 'reactstrap';

export const ToolComponent = (props) => {
    const { wrapperStyle, placement, target, toolContent, componetContent, Component, ...rest } = props;
    return (
        <span style={wrapperStyle}>
            <Component id={target} {...rest} >
                {componetContent}
            </Component>
            <UncontrolledTooltip placement={placement} target={target}>
                {toolContent}
            </UncontrolledTooltip>
        </span>
    )
}

export default ToolComponent;