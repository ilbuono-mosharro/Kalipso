document.getElementById("id_categories").addEventListener("change", function () {
    const elements = [
        "id_condition", "id_transmissions", "id_fuels", "id_ad_types", "schedule_id", "id_levels", "id_price_min",
        "id_price_max"
    ];
    for (let i = 0; i < elements.length; i++) {
        const element = document.getElementById(elements[i]);
        if (element) {
            document.getElementById(elements[i]).value = "";
        }
    }
});