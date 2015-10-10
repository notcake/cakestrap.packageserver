var VerticalCenter = React.createClass(
	{
		render: function()
		{
			return (
				<div style={ Object.assign({}, this.props.style || {}, { display: "table", height: "100%" }) }>
					<div style={ { display: "table-cell", verticalAlign: "middle", height: "100%" } }>
						{ this.props.children }
					</div>
				</div>
			);
		}
	}
);
