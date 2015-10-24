var PackageGridListViewItem = React.createClass(
	{
		render: function()
		{
			return (
				<div style={{ backgroundColor: "beige" } }>
					<a className="block" href={ "/packages/" + this.props.item.id } style={ { display: "block", overflow: "auto", width: "100%", padding: "8px" } }>
						<div className="col-md-4" style={ { width: "auto", marginRight: "4px" } }>
							<Icon icon="brick" />
						</div>
						<div style={ { float: "left", margin: "0px 0px" } }>
							<span style={ { fontSize: "110%", verticalAlign: "middle" } }>{ this.props.item.displayName }</span>
						</div>
					</a>
				</div>
			);
		}
	}
);

PackageGridListViewItem = StyleDecorator(PackageGridListViewItem);
