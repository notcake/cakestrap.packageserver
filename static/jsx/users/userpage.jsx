var UserPage = React.createClass(
	{
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<h2>{ this.props.user.displayName }</h2>
					<hr />
					<div style={ { overflow: "auto", width: "100%", margin: "8px auto", padding: "16px", backgroundColor: "beige" } }>
						<div className="col-md-3" style={ { width: "auto", marginRight: "16px" } }>
							<img src={ this.props.user.largeProfilePictureUrl } />
						</div>
						<div>
							<h2>{ this.props.user.displayName }</h2>
							<div style={ { marginTop: "2px", paddingLeft: "4px", color: "gray" } }>
								(<img src={ this.props.user.getRankIcon() } style={ { verticalAlign: "top", margin: "0px 2px" } } />{ this.props.user.getRankName() })
							</div>
						</div>
					</div>
				</div>
			);
		}
	}
);
