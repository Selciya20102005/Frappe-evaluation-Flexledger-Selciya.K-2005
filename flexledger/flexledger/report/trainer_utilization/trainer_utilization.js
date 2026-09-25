// Copyright (c) 2026, selciya and contributors
// For license information, please see license.txt

frappe.query_reports["Trainer Utilization"] = {
	filters: [
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"fieldname": "trainer",
			"label": "Trainer",
			"fieldtype": "Link",
			"options":"Trainer"
		},
	],
formatter:function(value,row,column,data){
	if(column.fieldname==="no_show_rate"){
		if (value>25){
			return`<span style="color:red">${value}%</span>`
		}
		if(value<10){
			return `<span style="color:green">${value}%</span>`
		}
	}
	return value;

}
};
