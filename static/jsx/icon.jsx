var Icon = React.createClass(
	{
		render: function()
		{
			var icon = this.props.icon;
			
			if (icon == "spinner")
			{
				return <Spinner />;
			}
			
			if (/[a-zA-Z0-9_]/.test(icon))
			{
				icon = "/static/images/silkicons/" + icon + ".png";
			}
			
			return <img src={ icon } style={ { verticalAlign: "middle" } } />;
		}
	}
);

Icon = StyleDecorator(Icon);
