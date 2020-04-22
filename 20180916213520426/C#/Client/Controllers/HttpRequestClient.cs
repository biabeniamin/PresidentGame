using Newtonsoft.Json;
using System;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace DatabaseFunctionsGenerator
{
    public static class HttpRequestClient
    {
        public static string ServerUrl
        {
            get
            {
                return "http://codeforgood18.avramiancuturda.ro/";
            }
        }
        public static async Task<string> GetRequest(string url)
        {
            var httpClient = new HttpClient();
            string response = "null";

            try
            {
                var uri = new Uri(ServerUrl + url);
                Console.WriteLine($"Attempting to fetch data from {uri.AbsoluteUri}");
                response = await httpClient.GetStringAsync(uri);
                Console.WriteLine($"Data from {uri.AbsoluteUri} {response}");

            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nException: {ex.Message}");
                Console.WriteLine($"\nStack Trace: {ex.StackTrace}");
            }

            return response;

        }

        public static async Task<string> PostRequest(string url, object jsonObject)
        {
            String responseString;
            var request = (HttpWebRequest)WebRequest.Create(ServerUrl + url);

            var postData = JsonConvert.SerializeObject(jsonObject);
            var data = Encoding.ASCII.GetBytes(postData);

            request.Method = "POST";
            request.ContentType = "application/x-www-form-urlencoded";
            request.ContentLength = data.Length;

            using (var stream = request.GetRequestStream())
            {
                stream.Write(data, 0, data.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();


            using (Stream stream = response.GetResponseStream())
            {
                StreamReader reader = new StreamReader(stream, Encoding.UTF8);
                responseString = reader.ReadToEnd();
            }

            return responseString;
        }
    }
}
