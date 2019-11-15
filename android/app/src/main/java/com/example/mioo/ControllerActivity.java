package com.example.mioo;

import android.os.AsyncTask;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

public class ControllerActivity extends AppCompatActivity {

    String toastMessage; // 눌린 버튼에 따른 toast 메세지 출력
    private AlertDialog dialog; // 알림창

    int next = 0;
    int previous = 0;

    Button nextButton;
    Button previousButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_controller);

        nextButton = findViewById(R.id.nextButton);
        previousButton = findViewById(R.id.previousButton);

        new ControllerActivity.BackgroundTask().execute();


        nextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                next = 1;
                toastMessage = "NEXT";
                sendRequest();
            }
        });
        previousButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                previous = 1;
                toastMessage = "PREVIOUS";
                sendRequest();
            }
        });



        if(AppHelper.requestQueue == null){
            //리퀘스트큐 생성 (MainActivit가 메모리에서 만들어질 때 같이 생성이 될것이다.
            AppHelper.requestQueue = Volley.newRequestQueue(getApplicationContext());
        }


    }


    public void sendRequest(){ // 데이터를 서버에 전송하는 함수 - 각 버튼에 대한 정보를 한 번에 전송
        String url = "http://10.0.2.2:8000/clothes/RemoteControl";
        //String url = "http://127.0.0.1:8000/clothes/RemoteControl";

        //StringRequest를 만듬 (파라미터구분을 쉽게하기위해 엔터를 쳐서 구분하면 좋다)
        //StringRequest는 요청객체중 하나이며 가장 많이 쓰인다고한다.
        //요청객체는 다음고 같이 보내는방식(GET,POST), URL, 응답성공리스너, 응답실패리스너 이렇게 4개의 파라미터를 전달할 수 있다.(리퀘스트큐에 )
        //화면에 결과를 표시할때 핸들러를 사용하지 않아도되는 장점이있다.
        StringRequest request = new StringRequest(Request.Method.POST, url, new Response.Listener<String>() {  //응답을 문자열로 받아서 여기다 넣어달란말임(응답을 성공적으로 받았을 떄 이메소드가 자동으로 호출됨
            @Override
            public void onResponse(String response) {
                Log.e("응답 => "+ response, "응답 => ");

                try {
                    JSONObject jsonResponse = new JSONObject(response);
                    boolean success = jsonResponse.getBoolean("success");
                    if (success) {// 서버로부터의 json응답이 success인 경우(전송이 정상적으로 이루어진 경우)
                        Toast.makeText(getApplicationContext(), toastMessage, Toast.LENGTH_SHORT).show(); // 서버에 전송이 성공한 경우 해당 토스트메시지 출력
                        next = 0;
                        previous = 0;

                    } else {
                        Toast.makeText(getApplicationContext(), "전송 실패", Toast.LENGTH_SHORT).show();
                    }
                    String response1 = jsonResponse.getString("next");
                    Log.e("response next => "+ response1, "response next => ");

                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        },
                new Response.ErrorListener(){ //에러발생시 호출될 리스너 객체
                    @Override
                    public void onErrorResponse(VolleyError error) {

                        Log.e("에러 => "+ error.getMessage(), "에러 => ");
                    }
                }
        ){
            //만약 POST 방식에서 전달할 요청 파라미터가 있다면 getParams 메소드에서 반환하는 HashMap 객체에 넣어줍니다.
            //이렇게 만든 요청 객체는 요청 큐에 넣어주는 것만 해주면 됩니다.
            //POST방식으로 안할거면 없어도 되는거같다.
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String, String> params = new HashMap<String, String>();

                params.put("next", next + "");
                params.put("previous", previous + "");

                return params;


            }

        };

        //아래 add코드처럼 넣어줄때 Volley라고하는게 내부에서 캐싱을 해준다, 즉, 한번 보내고 받은 응답결과가 있으면
        //그 다음에 보냈을 떄 이전 게 있으면 그냥 이전거를 보여줄수도  있다.
        //따라서 이렇게 하지말고 매번 받은 결과를 그대로 보여주기 위해 다음과같이 setShouldCache를 false로한다.
        //결과적으로 이전 결과가 있어도 새로 요청한 응답을 보여줌
        request.setShouldCache(false);
        AppHelper.requestQueue.add(request);


    }


    class BackgroundTask extends AsyncTask<Void, Void, String>
    {
        String target;

        @Override
        protected void onPreExecute(){
            try{
                target = "http://10.0.2.2:8000/clothes/RemoteControl"; // GET 방식
            }catch (Exception e){
                e.printStackTrace();
            }

        }
        @Override
        protected String doInBackground(Void... voids) {
            try{
                URL url = new URL(target);
                HttpURLConnection httpURLConnection = (HttpURLConnection)url.openConnection();
                InputStream inputStream = httpURLConnection.getInputStream(); // 넘어오는 결과값들을 저장
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream)); // 해당 inputstream에 있는 내용들을 버퍼에 담아 읽을수 있도록 함.
                String temp;
                StringBuilder stringBuilder = new StringBuilder(); // 문자열 형태로 저장
                while ((temp = bufferedReader.readLine()) != null){  // 버퍼에서 받아오는 값을 한줄씩 읽으면 temp에 저장
                    stringBuilder.append(temp + "\n");
                }
                bufferedReader.close();
                inputStream.close();
                httpURLConnection.disconnect();
                return stringBuilder.toString().trim();

            }catch (Exception e){
                e.printStackTrace();
            }

            return null;
        }

        @Override
        public void onProgressUpdate(Void... values){
            super.onProgressUpdate();
        }

        @Override
        public void onPostExecute(String result){ // 해당 결과 처리
            try{
                JSONObject jsonResponse = new JSONObject(result);
                boolean success = jsonResponse.getBoolean("success");
                if (success) {// 서버로부터의 json응답이 success인 경우(전송이 정상적으로 이루어진 경우)

                    Toast.makeText(getApplicationContext(), "소켓 연결 성공", Toast.LENGTH_SHORT).show(); // 서버에 전송이 성공한 경우 해당 토스트메시지 출력
                } else {
                    Toast.makeText(getApplicationContext(), "소켓 연결 실패", Toast.LENGTH_SHORT).show();
                }
                String nextResponse = jsonResponse.getString("next");
                String previousResponse = jsonResponse.getString("previous");
                Log.e("nextResponse => "+ nextResponse, "nextResponse => ");
                Log.e("nextResponse => "+ previousResponse, "nextResponse => ");




            }catch (Exception e){


                e.printStackTrace();
            }
        }

    }

}
