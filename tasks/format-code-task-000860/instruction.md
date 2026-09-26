Ensure ES index names are lowercase
With https://github.com/elastic/beats/pull/18854 libbeat changed the default behavior for not not lowercasing all outputs by default, but instead setting index and pipeline names to lowercase in the standard idxmgmt implementation. 
APM Server diverges from beats idxmgmt implementation, therefore APM Server would have needed to also update to this behavior. By not applying any change in APM Server but ugrading to libbeat changes, we introduced a regression where customized index names are no longer guaranteed to be lower case. 

Issue was reported in https://discuss.elastic.co/t/index-name-must-be-lowercase-after-upgrade-to-7-9-2/251433/7
