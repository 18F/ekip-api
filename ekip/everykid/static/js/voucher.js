$(document).ready(function() {

  var recordLocator = $('.voucher-barcode'),
      defaultID = $(recordLocator).find('.voucher-barcode-id').text(),
      randomNumber = Math.round(Math.random() * 9999999 - 1000000) + 1000000,
      randomID = randomNumber.toString();

  $(recordLocator).find('.voucher-barcode-id').remove();
  $(recordLocator).find("img").JsBarcode(randomID,{format:"CODE128",displayValue:true,fontSize:20, height:40});

  $(".voucher-barcode-image").JsBarcode(randomID,{format:"CODE128",displayValue:true,fontSize:20, height:40});


});
