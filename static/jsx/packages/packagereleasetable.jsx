var PackageReleaseTable = React.createClass(
	{
		render: function()
		{
			if (this.props.items == null ||
			    this.props.items.length == 0)
			{
				return (
					<ContentBox>
						<Placeholder text="There have been no package releases" />
					</ContentBox>
				);
			}
			
			return (
				<ColoredBox>
					{
						this.props.items.map(
							function(packageRelease)
							{
								return <PackageReleaseTableRow ref={ packageRelease.id } package={ this.props.package } item={ packageRelease } />
							}.bind(this)
						)
					}
				</ColoredBox>
			);
		}
	}
);
