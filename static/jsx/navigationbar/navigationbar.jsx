var NavigationBar = React.createClass(
	{
		render: function()
		{
			return (
				<div className="navigation-bar" style={ { height: "56px" } }>
					<VerticalCenter style={ { float: "left" } }>
						<a href="/" className="block" style={ { height: "100%", paddingLeft: "8px", paddingRight: "8px" } }>
							<VerticalCenter>
								<h1 style={ { margin: "0px" } }>Cakestrap Packages</h1>
							</VerticalCenter>
						</a>
					</VerticalCenter>
					<VerticalCenter style={ { float: "right", textAlign: "right" } }>
						{
							this.props.user ?
								<div style={ { display: "inline", color: "white" } }>
									<a href={ "/users/" + this.props.user.steamId64 } className="block" style={ { verticalAlign: "middle", height: "100%", paddingLeft: "8px", paddingRight: "8px" } }>
										<VerticalCenter>
											<img src={ this.props.user.smallProfilePictureUrl } style={ { marginRight: "4px" } } />
											{ this.props.user.displayName }
										</VerticalCenter>
									</a>
									{ " | " }
									<a href="/logout" className="block" style={ { verticalAlign: "middle", height: "100%", paddingLeft: "8px", paddingRight: "8px" } }>
										<VerticalCenter>Log out</VerticalCenter>
									</a>
								</div> :
								<a href="/login" style={ { marginRight: "8px" } }>
									<img src="https://steamcommunity-a.akamaihd.net/public/images/signinthroughsteam/sits_large_noborder.png" alt="Sign in through STEAM" />
								</a>
						}
					</VerticalCenter>
					<div style={ { margin: "auto", width: "50%", height: "100%", textAlign: "center" } }>
						<NavigationBarButton href="/packages/all" text="Packages" selected={ window.location.pathname.startsWith("/packages/") } />
						<NavigationBarButton href="/users/all" text="Users" selected={ window.location.pathname.startsWith("/users/") } />
					</div>
				</div>
			);
		}
	}
);
