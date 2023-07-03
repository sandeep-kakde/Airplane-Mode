// Copyright (c) 2023, Sandeep Kakde and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
        frm.add_custom_button(
            __("Assign Seat"),
            function () {
                frm.trigger("show_seat_assignment");
            },
            __("Actions")
        );
	},

    show_seat_assignment: function (frm) {
        let d = new frappe.ui.Dialog({
            title: 'Enter details',
            fields: [
                {
                    label: 'Seat Number',
                    fieldname: 'seat_number',
                    fieldtype: 'Data'
                }
            ],
            size: 'small',
            primary_action_label: 'Assign',
            primary_action(values) {
                console.log(values);
                if (values && values.seat_number) {
                    console.log(values.seat_number);
                    frm.set_value("seat", values.seat_number);
                }
                d.hide();
            }
        });
        d.show();
    }
});