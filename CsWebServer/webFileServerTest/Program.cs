using System;
using System.IO;
using System.Net;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        
        HttpListener listener = new HttpListener();
        listener.Prefixes.Add("http://localhost/");
        listener.Start();
        while (true)
        {
            HttpListenerContext context = listener.GetContext();
            HttpListenerResponse res = context.Response;
            res.StatusCode = 200;
            byte[] content = Encoding.UTF8.GetBytes("HELLO");
            res.OutputStream.Write(content, 0, content.Length);
            res.Close();
        }
    }
}