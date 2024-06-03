export const ERROR_CODE_TYPE = (code: string): string => {
  let errMessage = 'Error';
  switch (Number(code)) {
    case 400:
      errMessage = 'Bad Request';
      break;
    case 401:
      errMessage = 'Unauthorized, please login again';
      break;
    case 403:
      errMessage = 'Forbidden';
      break;
    case 404:
      errMessage = 'Not Found';
      break;
    case 405:
      errMessage = 'Method Not Allowed';
      break;
    case 408:
      errMessage = 'Request Timeout';
      break;
    case 500:
      errMessage = 'Internal Server Error';
      break;
    case 501:
      errMessage = 'Not Implemented';
      break;
    case 502:
      errMessage = 'Bad Gateway';
      break;
    case 503:
      errMessage = 'Service Unavailable';
      break;
    case 504:
      errMessage = 'Gateway Timeout';
      break;
    case 505:
      errMessage = 'HTTP Version Not Supported';
      break;
    default:
      errMessage = 'Other Connection Error';
  }
  return `${code}: ${errMessage}`;
};