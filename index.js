function exportHTML(){
  var header = "<html xmlns:o='urn:schemas-microsoft-com:office:office' "+
       "xmlns:w='urn:schemas-microsoft-com:office:word' "+
       "xmlns='http://www.w3.org/TR/REC-html40'>"+
       "<head><meta charset='utf-8'><title>Export HTML to Word Document with JavaScript</title></head><body>";
  var footer = "</body></html>";
  var sourceHTML = header+document.getElementById("book-page-download").innerHTML+footer;
  
  var source = 'data:application/vnd.ms-word;charset=utf-8,' + encodeURIComponent(sourceHTML);
  var fileDownload = document.createElement("a");
  document.body.appendChild(fileDownload);
  fileDownload.href = source;
  fileDownload.download = 'document.doc';
  fileDownload.click();
  document.body.removeChild(fileDownload);
}

function addTabSpaces(strings, numSpaces) {
  // Check if numSpaces is a positive integer
  if (!Number.isInteger(numSpaces) || numSpaces < 0) {
      throw new Error('Number of spaces must be a positive integer.');
  }

  // Add tab spaces to each string in the array
  const result = strings.map(str => {
      // Create a string with the desired number of spaces
      const spaces = '&nbsp;'.repeat(numSpaces);
      // Concatenate the spaces with the original string
      return spaces + str;
  });
  console.log(`result: ${result}`);
  return result;
}


