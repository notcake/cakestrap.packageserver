var FieldContent = React.createClass(
	{
		render: function()
		{
			return (
				<div className="col-md-9">
					{ this.props.children }
				</div>
			);
		}
	}
);

FieldContent = StyleDecorator(FieldContent);
