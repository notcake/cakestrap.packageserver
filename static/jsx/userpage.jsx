var UserPage = React.createClass(
	{
		getInitialState: function()
		{
			return {
				rankIcons: {
					user:          "silkicons/user.png",
					moderator:     "silkicons/shield.png",
					administrator: "silkicons/shield.png",
					overlord:      "steam/emoticons/roar.png"
				},
				
				rankNames: {
					user:          "Peasant Scrub",
					moderator:     "Moderator",
					administrator: "Thought Police",
					overlord:      "Reptilian Overlord"
				}
			};
		},
		
		render: function()
		{
			return (
				<div>
					<div style={ { overflow: "auto", width: "50%", margin: "8px auto", padding: "16px", backgroundColor: "beige" } }>
						<div className="col-md-3" style={ { width: "auto", marginRight: "16px" } }>
							<img src={ this.props.user.largeProfilePictureUrl } />
						</div>
						<div>
							<h2>{ this.props.user.displayName }</h2>
							<div style={ { marginTop: "2px", paddingLeft: "4px", color: "gray" } }>
								(<img src={ "/static/images/" + this.state.rankIcons[this.props.user.rank] } style={ { verticalAlign: "top", margin: "0px 2px" } } />{ this.state.rankNames[this.props.user.rank] })
							</div>
						</div>
					</div>
				</div>
			);
		}
	}
);
