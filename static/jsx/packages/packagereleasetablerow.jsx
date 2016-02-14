var PackageReleaseTableRow = React.createClass(
	{
		getInitialState: function()
		{
			return { hovered: false }
		},
		
		render: function()
		{
			return (
				<ColoredBox className="striped" onMouseEnter={ this.handleMouseEnter } onMouseLeave={ this.handleMouseLeave }>
					<TableRowButton visible={ this.state.hovered && currentUser.canDeletePackageRelease(this.props.package, this.props.item) } icon="cross"      href={ this.props.item.getBasePath() + "/delete?returnPage=package" } />
					<TableRowButton visible={ this.state.hovered                                                                             } icon="basket_put" href={ this.props.item.getBasePath() + "/download"                  } />
					<a className="block" href={ this.props.item.getBasePath() } style={ { display: "block", overflow: "auto", padding: "8px", position: "relative" } }>
						<div style={ { float: "left", marginRight: "8px" } }>
							<Icon icon="brick" />
						</div>
						<div style={ { float: "left", margin: "0px 0px" } }>
							{ this.props.item.fileName }
						</div>
					</a>
				</ColoredBox>
			);
		},
		
		handleMouseEnter: function()
		{
			this.setState({ hovered: true });
		},
		
		handleMouseLeave: function()
		{
			this.setState({ hovered: false });
		}
	}
);

PackageReleaseTableRow = StyleDecorator(PackageReleaseTableRow);
