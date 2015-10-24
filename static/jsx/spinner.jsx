var Spinner = React.createClass(
	{
		render: function()
		{
			return <span className="fa fa-cog fa-spin" style={ { lineHeight: "0px", verticalAlign: "middle", fontSize: "120%", color: this.props.color || "orange" } }/>;
		}
	}
);

Spinner = StyleDecorator(Spinner);
