var UserGridListViewItem = React.createClass(
	{
		render: function()
		{
			return (
				<ColoredBox key={ this.props.item.id }>
					<a className="block" href={ this.props.item.getBasePath() } style={ { display: "block", overflow: "auto", width: "100%", padding: "8px" } }>
						<div style={ { float: "left", marginRight: "8px" } }>
							<img src={ this.props.item.mediumProfilePictureUrl } style={ { width: "48px", height: "48px", borderRadius: "3px" } } />
						</div>
						<div style={ { float: "left", margin: "0px 0px" } }>
							<span style={ { fontSize: "110%" } }>{ this.props.item.displayName }</span>
							<br />
							<span style={ { color: "gray" } }>
								(<img src={ this.props.item.getRankIcon() } style={ { verticalAlign: "top", margin: "0px 2px" } } />{ this.props.item.getRankName() })
							</span>
						</div>
					</a>
				</ColoredBox>
			);
		}
	}
);

UserGridListViewItem = StyleDecorator(UserGridListViewItem);
