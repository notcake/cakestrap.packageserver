var NavigationBarButton = React.createClass(
	{
		render: function()
		{
			return (
				<a
					href={ this.props.href }
					className="block"
					style={
						Object.assign(
							{ height: "100%", paddingLeft: "16px", paddingRight: "16px" },
							this.props.selected ? { paddingTop: "4px", borderBottom: "4px solid rgba(255, 255, 255, 0.5)" } : {}
						)
					}
				>
					<VerticalCenter><b>{ this.props.text }</b></VerticalCenter>
				</a>
			);
		}
	}
);
