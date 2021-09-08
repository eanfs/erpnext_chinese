frappe.listview_settings['Quality Inspection'] = {
    formatters:{
        inspection_type: function(value, df, doc) {
            const custom_translation = {"Incoming":"来料检验",
                                        "Outgoing":"出货检验",
                                        "In Process":"制程检验"
                        };
            if (frappe.boot.lang === 'zh'){
                const translated = custom_translation[doc["inspection_type"]];            
                value = translated? translated: value;
            }
            return value;
        }
    }
}