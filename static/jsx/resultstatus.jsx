var ResultStatus = React.createClass(
	{
		render: function()
		{
			if (!this.props.resultState)
			{
				return null;
			}
			
			return (
				<span className={ this.props.resultState.toClassName() }>
					<Icon icon={ this.props.resultState.toIcon() } visible={ this.props.resultState.toVisibility() } />
					<span className="control-label" style={ { verticalAlign: "middle", marginLeft: this.props.resultState.getMessage() ? "4px" : "0px" } }>
						{ this.props.resultState.getMessage() }
					</span>
				</span>
			);
		}
	}
);

ResultStatus = StyleDecorator(ResultStatus);
