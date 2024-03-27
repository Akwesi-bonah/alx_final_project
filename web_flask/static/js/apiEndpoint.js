const API_ENDPOINTS = "http://127.0.0.1:5003/api/v1/";
//const API_ENDPOINTS = 'https://www.aflahgh.tech/api/';
//const API_ENDPOINTS = 'https://app.aflahgh.tech/api/v1/';

const showloader = () => {
    Swal.fire({
      title: "Processing...Please wait!",
      onBeforeOpen: () => {
        Swal.showLoading();
      },
    });
  };
  
export default API_ENDPOINTS;
