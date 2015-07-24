$(document).ready(function() {

  var recordLocator = $('.voucher-barcode'),
      locatorID = $(recordLocator).find('.voucher-barcode-id').text();

  $(recordLocator).find('.voucher-barcode-id').remove();
  $(recordLocator).find("img").JsBarcode(locatorID,{format:"CODE128",displayValue:true,fontSize:20, height:40});

  $(".voucher-barcode-image").JsBarcode(locatorID,{format:"CODE128",displayValue:true,fontSize:20, height:40});

});
