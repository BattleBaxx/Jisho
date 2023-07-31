export const request = async function (queryData) {
  console.log("Query data is: ", queryData);
  const response = await fetch("http://localhost:8080/search/v1/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(queryData),
  });
  return response.json();
};
