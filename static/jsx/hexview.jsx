var HexView = React.createClass(
	{
		getInitialState: function()
		{
			return { data: this.props.data };
		},
		
		render: function()
		{
			var lineAddresses = [];
			var hexLines      = [];
			var textLines     = [];
			
			if (this.state.data)
			{
				var uint8Array = new Uint8Array(this.state.data);
				var bytesPerLine = 24;
				
				for (var i = 0; i < uint8Array.length; i += bytesPerLine)
				{
					var address = i.toString(16);
					while (address.length < 8) { address = "0" + address; }
					lineAddresses.push(address + " ");
				}
				
				var hexLine  = "";
				var textLine = "";
				
				var i = 0;
				for (i = 0; i < uint8Array.length; i++)
				{
					if (i % bytesPerLine == 0)
					{
						if (hexLine.length  > 0) { hexLines.push(hexLine + " "); }
						if (textLine.length > 0) { textLines.push(" " + textLine); }
						hexLine  = "";
						textLine = "";
					}
					
					var hex = uint8Array[i].toString(16);
					while (hex.length < 2) { hex = "0" + hex; }
					
					if (uint8Array[i] == 0)
					{
						hex = "<span style=\"color: gray\">" + hex + "</span>";
					}
					
					if (i % bytesPerLine != 0)
					{
						if (i % 4 == 0 && i > 0)
						{
							hex = " " + hex;
						}
					}
					hexLine += " " + hex;
					
					// ASCII
					if ((0x20 <= uint8Array[i] && uint8Array[i] < 0x7F) ||
					    (0xA1 <= uint8Array[i] && uint8Array[i] <= 0xFF))
					{
						var c = String.fromCodePoint(uint8Array[i]);
						if (c == "&") { c = "&amp;"; }
						if (c == "<") { c = "&lt;"; }
						if (c == ">") { c = "&gt;"; }
						if (c == "\"") { c = "&quot;"; }
						textLine += c;
					}
					else
					{
						if (uint8Array[i] == 0)
						{
							textLine += "<span style=\"color: gray\">.</span>";
						}
						else
						{
							textLine += ".";
						}
					}
				}
				
				while (i % bytesPerLine != 0 || i < bytesPerLine)
				{
					var hex = "  ";
					if (i % 4 == 0 && i > 0) { hex = " " + hex; }
					hexLine += " " + hex;
					textLine += " ";
					
					i++;
				}
				
				hexLines.push(hexLine + " ");
				textLines.push(" " + textLine);
			}
			
			return (
				<pre style={ { margin: "0px" } }>
					<div style={ { display: "inline-block", borderRight: "1px solid black" } }>
						{ lineAddresses.join("\n") }
					</div>
					<div style={ { display: "inline-block", borderRight: "1px solid black" } } dangerouslySetInnerHTML={ { __html: hexLines.join("\n") } } />
					<div style={ { display: "inline-block" } } dangerouslySetInnerHTML={ { __html: textLines.join("\n") } } />
				</pre>
			);
		},
		
		componentWillReceiveProps: function(nextProps)
		{
			if (this.props.data != nextProps.data)
			{
				this.setData(nextProps.data);
			}
		},
		
		setData: function(data)
		{
			AAA = data;
			this.setState({ data: data });
		}
	}
);
