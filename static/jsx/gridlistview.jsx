var GridListView = React.createClass(
	{
		render: function()
		{
			var visibleItemCount = 0;
			
			return (
				<div
					className={ this.props.viewMode == "grid" ? "grid-view" : "list-view" }
					style={ { overflow: "auto", textAlign: "center" } }
				>
					<div style={ this.props.viewMode == "grid" ? { display: "inline", textAlign: "left" } : null }>
						{
							this.props.items.map(
								function(item)
								{
									visibleItemCount = visibleItemCount + 1;
									
									return (
										<div
											key={ item.id }
											className={ this.props.viewMode == "grid" ? "grid-view-item" : "list-view-item" }
										>
											<this.props.itemClass items={ this.props.items } item={ item } />
										</div>
									);
								}.bind(this)
							)
						}
						{
							this.props.viewMode == "grid" &&
							visibleItemCount % 3 != 0 &&
							visibleItemCount % 3 <= 1 ?
								<div className="grid-view-item" /> :
								null
						}
						{
							this.props.viewMode == "grid" &&
							visibleItemCount % 3 != 0 &&
							visibleItemCount % 3 <= 2 ?
								<div className="grid-view-item" /> :
								null
						}
					</div>
				</div>
			);
		}
	}
);

GridListView = StyleDecorator(GridListView);
