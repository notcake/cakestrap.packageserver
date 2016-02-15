var Knotcake = Knotcake || {};

var self = {};
Knotcake.DateTime = Knotcake.OOP.Class(self);

self.ctor = function(timestamp)
{
	this.timestamp = timestamp;
	this.date = new Date(timestamp * 1000);
};

self.getMonthName = function()
{
	switch (this.date.getMonth())
	{
		case 0:  return "January";
		case 1:  return "February";
		case 2:  return "March";
		case 3:  return "April";
		case 4:  return "May";
		case 5:  return "June";
		case 6:  return "July";
		case 7:  return "August";
		case 8:  return "September";
		case 9:  return "October";
		case 10: return "November";
		case 11: return "December";
	}
	
	return "Unknown";
};

self.getTimestamp = function()
{
	return this.timestamp;
};

self.toShortLocalTimeString = function()
{
	return this.date.getHours() + ":" + this.date.getMinutes();
};

self.toLongLocalTimeString = function()
{
	return this.toShortLocalTimeString() + ":" + this.date.getSeconds();
};

self.toLongLocalString = function()
{
	return this.toLongLocalDateString() + " " + this.toLongLocalTimeString();
};

self.toLongLocalDateString = function()
{
	return this.date.getDate() + " " + this.getMonthName() + " " + this.date.getFullYear();
};

self.toRelativeTimeString = function()
{
	var timeUnits = [
		{ duration:                  0.001, name: "millisecond" },
		{ duration:                  1,     name: "second"      },
		{ duration:                 60,     name: "minute"      },
		{ duration:            60 * 60,     name: "hour"        },
		{ duration:       24 * 60 * 60,     name: "day"         },
		{ duration: 365 * 24 * 60 * 60,     name: "year"        },
	];
	
	var dt = Date.now() / 1000 - this.timestamp;
	var future = dt < 0;
	if (future) { dt = -dt; }
	
	var timeUnitIndex = 0;
	while (timeUnitIndex < timeUnits.length &&
	       timeUnits[timeUnitIndex].duration <= dt)
	{
		timeUnitIndex++;
	}
	timeUnitIndex--;
	if (timeUnitIndex < 0) { timeUnitIndex++; }
	
	var timeString = "";
	
	// First unit
	var unitCount = Math.floor(dt / timeUnits[timeUnitIndex].duration);
	dt = dt - unitCount * timeUnits[timeUnitIndex].duration;
	timeString += unitCount + " " + timeUnits[timeUnitIndex].name;
	if (unitCount != 1) { timeString += "s"; }
	
	// Second unit
	timeUnitIndex--;
	if (dt > 0 && timeUnitIndex >= 0)
	{
		timeString += ", ";
		
		var unitCount = Math.floor(dt / timeUnits[timeUnitIndex].duration);
		dt = dt - unitCount * timeUnits[timeUnitIndex].duration;
		timeString += unitCount + " " + timeUnits[timeUnitIndex].name;
		if (unitCount != 1) { timeString += "s"; }
	}
	
	return future ? ("in " + timeString) : (timeString + " ago");
};
