# Bloodhound
A Python Tool Box that helps ArcGIS Users find records and zooms to the selected feature.  It is a simplified select by attribute.  

It creates three inputs: feature, field, and record.  The feature and field inputs are drop downs; the record is a text input.  

The record input with match the data type of the field:

* String is an exact match but not case sensitive
* Integer is an exact match
* Float is  limited need a between method
* Date is between method with syntax year month date (xxxx xx xx)
