var Button = React.createClass(
	{
		render: function()
		{
			return (
				<a href={ this.props.href || "#" } className="btn btn-default" onClick={ this.handleClick }>
					{
						this.props.icon ?
							<Icon icon={ this.props.icon } style={ { verticalAlign: "middle", marginRight: "4px" } } />:
							null
					}
					{
						this.props.text ?
							<span style={ { verticalAlign: "middle" } }>{ this.props.text }</span> :
							null
					}
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
