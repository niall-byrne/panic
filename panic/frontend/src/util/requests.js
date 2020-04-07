export function get(path) {
  let statusCode;

  const headers = {
    'Accept': 'application/json',    
  } 
  const promise = fetch(
    `${process.env.BASE_URL}${path}`, {
      method: "POST",
      headers
    })
    .then(fetchResponse => {
      statusCode = fetchResponse.status         
      return fetchResponse.json()
    })

  return {promise, statusCode}

};


export function post(path, data={}) {

  // eslint-disable-next-line no-console
  console.debug(`API POST:\n ${process.env.BASE_URL}${path}`)
  // eslint-disable-next-line no-console
  console.debug(`Content:\n ${JSON.stringify(data)}`)
  let statusCode;

  const headers = {
    'Accept': 'application/json',  
    'Content-Type': 'application/json'  
  } 
  const promise = fetch(
    `${process.env.BASE_URL}${path}`, {
      method: "POST",
      headers,
      body: JSON.stringify(data)
    })
    .then(fetchResponse => {
      const contentType = fetchResponse.headers.get('content-type');      
      statusCode = fetchResponse.status    
      if (contentType === null) return new Promise(() => null);  
      if (contentType.startsWith('application/json')) return fetchResponse.json();
      return fetchResponse.text()
    })
    .then(fetchResponseDecoded => { 
      // eslint-disable-next-line no-console
      console.debug(`API Response Status Code:\n ${statusCode}`)
      return [fetchResponseDecoded, statusCode]
    })
    .catch(() => {
      // eslint-disable-next-line no-console
      console.debug("API Error.")   
    });
    return promise;
};

export default get;
