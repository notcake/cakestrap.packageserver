var DirectoryTreeFieldsView = React.createClass(
	{
		render: function()
		{
			var type = this.props.item ? this.props.item.type : "none";
			
			var content = null;
			switch (type)
			{
				case "svn":  content = <SvnRepositoryTreeFieldsView item={ this.props.item } />; break;
				case "git":  content = <GitRepositoryTreeFieldsView item={ this.props.item } />; break;
				case "raw":  content = null; break;
				case "none": content = <Placeholder text="None" />; break;
				default:     content = null; break;
			}
			
			return <div>{ content }</div>;
		}
	}
);

var DirectoryTreeFieldsEditor = React.createClass(
	{
		render: function()
		{
			var type = this.props.item ? this.props.item.type : "none";
			
			var content = null;
			switch (type)
			{
				case "svn":  content = <SvnRepositoryTreeFieldsEditor ref="editor" item={ this.props.item } onEnter={ this.handleEnter } />; break;
				case "git":  content = <GitRepositoryTreeFieldsEditor ref="editor" item={ this.props.item } onEnter={ this.handleEnter } />; break;
				case "raw":  content = null; break;
				case "none": content = null; break;
				default:     content = null; break;
			}
			
			return (
				<div>
					<RadioButtonGroup value={ type } onValueChanged={ this.handleTypeChanged }>
						<RadioButton value="none" text="None" />
						<RadioButton value="svn"  text="SVN" />
						<RadioButton value="git"  text="Git" />
						<RadioButton value="raw"  text="Raw" />
					</RadioButtonGroup>
					<div style={ { marginTop: "8px" } }>
						{ content }
					</div>
				</div>
			);
		},
		
		focus: function(fieldName)
		{
			if (!this.refs.editor) { return; }
			
			this.refs.editor.focus(fieldName);
		},
		
		select: function(fieldName)
		{
			if (!this.refs.editor) { return; }
			
			this.refs.editor.select(fieldName);
		},
		
		validate: function(fieldName)
		{
			if (!this.refs.editor) { return; }
			
			this.refs.editor.validate(fieldName);
		},
		
		handleTypeChanged: function(type)
		{
			if (!this.props.item) { return; }
			if (this.props.item.type == type) { return; }
		
			this.props.item.type = type;
			this.forceUpdate();
		},
		
		handleEnter: function(event)
		{
			if (this.props.onEnter)
			{
				this.props.onEnter(event);
			}
		}
	}
);

