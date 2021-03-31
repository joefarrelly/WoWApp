var coll = document.getElementsByClassName("subnavbtn");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
} 

function boost(evt, boostType) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(boostType).style.display = "block";
    evt.currentTarget.className += " active";
}

$(document).ready(function () {
    // all custom jQuery will go here
    $("#boost-options-table tr:gt(0)").click(function () {
        $(this).addClass('selected').siblings().removeClass('selected');
        var value = $(this).find('td:first').html();
        document.getElementById("id_boostId").value = value;
        $('#delete-boost-button').removeAttr('disabled');
    });
    $("#accounts-table tr:gt(0)").click(function () {
        $(this).addClass('selected').siblings().removeClass('selected');
        var value = $(this).find('td:first').html();
        var tempVal = document.getElementsByName("userId");
        for (var i = 0; i < tempVal.length; i++) {
            tempVal[i].value = value;
        }
        $('#delete-account-button').removeAttr('disabled');
        $('#edit-account-button').removeAttr('disabled');

    });

    $(".delete-boost-form").submit(function () {
        if (confirm('Are you sure you want to delete the selected boost?')) {
            alert("Selected boost has been deleted successfully!");
            return true;
        } else {
            return false;
        }
    });

    $(".delete-account-form").submit(function () {
        if (confirm('Are you sure you want to delete the selected account?')) {
            alert("Selected account has been deleted successfully!");
            return true;
        } else {
            return false;
        }
    });

    $("#edit-account-form").submit(function() {
        alert("Account has been updated successfully!");
        return true;
    })

    $('#id_role-userRole').on('change', function () {
        $('#id_advRank').change();
        $('#id_advertiser-advRank').change();
        if (this.value === 'User') {
            $("#userData").show();
            $("#userRoleData").show();
            $("#advertiserData").hide();
            $("#boosterData").hide();
            $("#advertiserData :input").prop("disabled", true);
            $("#boosterData :input").prop("disabled", true);
        } else if (this.value === 'Advertiser') {
            $("#userData").show();
            $("#userRoleData").show();
            $("#advertiserData").show();
            $("#boosterData").hide();
            $("#advertiserData :input").prop("disabled", false);
            $("#boosterData :input").prop("disabled", true);
        } else if (this.value === 'Booster') {
            $("#userData").show();
            $("#userRoleData").show();
            $("#advertiserData").show();
            $("#boosterData").show();
            $("#advertiserData :input").prop("disabled", false);
            $("#boosterData :input").prop("disabled", false);
        }
    });
    $('#id_role-userRole').change();

    $('#id_advRank').on('change', function () {
        $("#id_advCommission").val(this.value * 0.04);
    });

    $('#id_advertiser-advRank').on('change', function () {
        $("#id_advertiser-advCommission").val(this.value * 0.04);
    });
});
