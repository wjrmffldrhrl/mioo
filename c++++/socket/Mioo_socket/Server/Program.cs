
using System;

using System.Collections.Generic;

using System.Linq;

using System.Text;

using System.Threading.Tasks;





using System.IO;

using System.Net;

using System.Net.Sockets;

using System.Threading;



namespace Sock_console_server

{

    class Receiver

    {

        NetworkStream NS = null;

        StreamReader SR = null;

        StreamWriter SW = null;

        TcpClient client;

        public void startClient(TcpClient clientSocket)

        {

            client = clientSocket;

            Thread echo_thread = new Thread(echo);

            echo_thread.Start();

        }



        public void echo()

        {

            NS = client.GetStream(); // 소켓에서 메시지를 가져오는 스트림

            SR = new StreamReader(NS, Encoding.UTF8); // Get message

            SW = new StreamWriter(NS, Encoding.UTF8); // Send message



            string GetMessage = string.Empty;

            try
            {
                Console.WriteLine("start connect");
                while (client.Connected == true) //클라이언트 메시지받기

                {

                    GetMessage = SR.ReadLine();
                    //GetMessage = SR.ReadToEnd();

                    //Console.WriteLine("get data");
                    SW.WriteLine("Server: {0} [{1}]", GetMessage, DateTime.Now); // 메시지 보내기

                    Console.WriteLine("Log: {0} [{1}]", GetMessage, DateTime.Now);
                    SW.Flush();
                    //Console.WriteLine("send data");

                }

            }

            catch (Exception ee)

            {



            }

            finally

            {

                Console.WriteLine("connection end");

                SW.Close();

                SR.Close();

                client.Close();

                NS.Close();

            }

        }

    }



    class Program

    {

        static void Main(string[] args)

        {

            TcpListener Listener = null;

            TcpClient client = null;



            int PORT = 10000;



            Console.WriteLine("서버소켓");

            try

            {

                Listener = new TcpListener(PORT);

                Listener.Start(); // Listener 동작 시작



                while (true)

                {

                    client = Listener.AcceptTcpClient();

                    Receiver r = new Receiver();

                    r.startClient(client);



                }

            }

            catch (Exception e)

            {

                System.Console.WriteLine(e.Message);

            }

            finally

            {

            }

        }

    }

}