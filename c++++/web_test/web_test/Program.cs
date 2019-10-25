using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.IO;

namespace web_test
{
    class Program
    {
        static void Main(string[] args)
        {
            string url = "http://kyu9341.pythonanywhere.com/uleung/raspberry/";  //테스트 사이트
            string responseText = string.Empty;

            while (true){

                HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
                request.Method = "GET";
                request.Timeout = 30 * 1000; // 30초
                request.Headers.Add("Authorization", "BASIC SGVsbG8="); // 헤더 추가 방법

                using (HttpWebResponse resp = (HttpWebResponse)request.GetResponse())
                {
                    HttpStatusCode status = resp.StatusCode;
                    Console.WriteLine(status);  // 정상이면 "OK"

                    Stream respStream = resp.GetResponseStream();
                    using (StreamReader sr = new StreamReader(respStream))
                    {
                        responseText = sr.ReadToEnd();
                    }
                }

                Console.WriteLine(responseText);
            }

        }
    }
}
