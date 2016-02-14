var PackageGridListViewItem = React.createClass(
	{
		render: function()
		{
			return (
				<ColoredBox>
					<a className="block" href={ this.props.item.getBasePath() } style={ { display: "block", overflow: "auto", width: "100%", padding: "8px" } }>
						<div style={ { float: "left", marginRight: "4px" } }>
							<Icon icon="brick" />
						</div>
						<div style={ { float: "left", margin: "0px 0px" } }>
							<span style={ { fontSize: "110%" } }>{ this.props.item.displayName }</span>
						</div>
					</a>
				</ColoredBox>
			);
		}
	}
);

PackageGridListViewItem = StyleDecorator(PackageGridListViewItem);
