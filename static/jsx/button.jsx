var Button = React.createClass(
	{
		render: function()
		{
			return (
				<a href={ this.props.href || "#" } className={ "btn btn-default" + (this.props.pressed ? " active" : "") } onClick={ this.handleClick }>
					{
						this.props.icon ?
							<Icon icon={ this.props.icon } style={ { verticalAlign: "middle", marginRight: this.props.text ? "4px" : "0px" } } />:
							null
					}
					<span style={ { verticalAlign: "middle" } }>{ this.props.text }</span>
					{ this.props.children }
				</a>
			);
		},
		
		handleClick: function(event)
		{
			if (!this.props.href)
			{
				event.preventDefault();
			}
			
			if (this.props.onClick)
			{
				this.props.onClick(event);
			}
		}
	}
);

Button = StyleDecorator(Button);
