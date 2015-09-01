$(document).ready(function() {

  $('.print button').click(function() {
    window.print();
  });

  var locatorID;

  $('.voucher-barcode').each(function() {

    locatorID = $(this).find('.barcode').attr('data-id');

    $(this).find('img').JsBarcode(locatorID, {
      format: 'CODE128',
      displayValue: true,
      fontSize: 33,
      height: 50
    });

  })

  $('.personnel').each(function() {

    locatorID = $(this).find('img').attr('data-id');

    $(this).find("img").JsBarcode(locatorID, {
      format: 'CODE128',
      displayValue: true,
      fontSize: 25,
      height: 50
    });

  });

});
