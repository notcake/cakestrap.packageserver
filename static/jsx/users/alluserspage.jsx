var AllUsersPage = React.createClass(
	{
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<h2>Users</h2>
					<hr />
					<GridListView viewMode="grid" itemClass={ UserGridListViewItem } items={ this.props.users } />
				</div>
			);
		}
	}
);
