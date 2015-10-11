var AllPackagesPage = React.createClass(
	{
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<div style={ { float: "right" } }>
						<Button href="/packages/create" icon="/static/images/silkicons/add.png" text="Add package" />
					</div>
					<h2>Packages</h2>
					<hr />
					<div style={ { textAlign: "center" } }>
						<div style={ { display: "inline", textAlign: "left" } }>
							{
								this.props.packages.map(
									function(user)
									{
										return (
											<div key={ user.id } style={ { display: "inline-block", width: "30%", margin: "8px 8px", backgroundColor: "beige" } }>
												<a className="block" href={ "/users/" + user.steamId64 } style={ { display: "block", overflow: "auto", width: "100%", padding: "8px" } }>
													<div className="col-md-4" style={ { width: "auto", marginRight: "8px" } }>
														<img src={ user.mediumProfilePictureUrl } style={ { width: "48px", height: "48px" } } />
													</div>
													<div style={ { float: "left", margin: "0px 0px" } }>
														<span style={ { fontSize: "110%" } }>{ user.displayName }</span>
														<br />
														<span style={ { color: "gray" } }>
															(<img src={ "/static/images/" + this.state.rankIcons[user.rank] } style={ { verticalAlign: "top", margin: "0px 2px" } } />{ this.state.rankNames[user.rank] })
														</span>
													</div>
												</a>
											</div>
										);
									}.bind(this)
								)
							}
							{
								this.props.packages.length % 3 != 0 &&
								this.props.packages.length % 3 <= 1 ?
									<div style={ { display: "inline-block", width: "30%", margin: "8px 8px" } } /> :
									null
							}
							{
								this.props.packages.length % 3 != 0 &&
								this.props.packages.length % 3 <= 2 ?
									<div style={ { display: "inline-block", width: "30%", margin: "8px 8px" } } /> :
									null
							}
						</div>
					</div>
				</div>
			);
		}
	}
);
