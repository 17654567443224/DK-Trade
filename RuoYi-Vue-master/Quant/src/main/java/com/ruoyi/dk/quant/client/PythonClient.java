package com.ruoyi.dk.quant.client;
import com.ruoyi.common.core.domain.AjaxResult;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;
@Component
public class PythonClient {
    private final RestTemplate restTemplate = new RestTemplate();
    @Value("${client.python.url}")
    private String url;
    @Value("${client.python.port}")
    private String port;
    private final String path = "/engine/simulation";
    /**
     * 发送数据到 Python 服务（POST）
     *
     * @param data 实体类对象
     * @return Python 服务返回的响应（Map 格式）
     */
    /**
     * 发送数据到 Python 服务（POST）
     *
     * @param data   请求参数（任意类型）
     * @param clazz  返回类型的 Class 对象
     * @param <T>    返回类型的泛型
     * @return 反序列化后的对象
     */
    public <T> T sendDataToPython(Object data, Class<T> clazz) {
        String url = "http://" + this.url + ":" + this.port + this.path;

        // 设置请求头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // 创建请求实体
        HttpEntity<Object> request = new HttpEntity<>(data, headers);

        // 发送 POST 请求并返回响应
        return restTemplate.postForObject(url, request, clazz);
    }

    /**
     * 从 Python 服务获取数据（GET）
     */
    public Map<String, Object> getDataFromPython() {
        String url = "http://" + this.url + ":" + this.port + this.path;
        return restTemplate.getForObject(url, Map.class);
    }

//    @PreAuthorize("@ss.hasAnyRoles('admin')")
//    public Map<String, Object> queryRunningStrategies(){
//        HashMap<String, String> data = new HashMap<>();
//        data.put("action", "running_strategies");
//        AjaxResult ajaxResult = new AjaxResult(0, "queryRunningStrategies", data);
//        return this.sendDataToPython(ajaxResult);
//    }
//
//    public Map<String, Object> addStrategy(String data){
//        HashMap<String, String> dt = new HashMap<>();
//        dt.put("action", "add_strategy");
//        dt.put("args", data);
//        AjaxResult ajaxResult = new AjaxResult(0, "add_strategy", dt);
//        return this.sendDataToPython(ajaxResult);
//    }
//
//    public Map<String, Object> removeStrategy(String data){
//        HashMap<String, String> dt = new HashMap<>();
//        dt.put("action", "remove_strategy");
//        dt.put("args", data);
//        AjaxResult ajaxResult = new AjaxResult(0, "add_strategy", dt);
//        return this.sendDataToPython(ajaxResult);
//    }
//
//    public Map<String, Object> runStrategy(String data){
//        HashMap<String, String> dt = new HashMap<>();
//        dt.put("action", "run_strategy");
//        dt.put("args", data);
//        AjaxResult ajaxResult = new AjaxResult(0, "runStrategy", dt);
//        return this.sendDataToPython(ajaxResult);
//    }
//
//    public Map<String, Object> operationInformation(String data){
//        HashMap<String, String> dt = new HashMap<>();
//        dt.put("action", "operation_information");
//        dt.put("args", data);
//        AjaxResult ajaxResult = new AjaxResult(0, "operationInformation", dt);
//        return this.sendDataToPython(ajaxResult);
//    }
//
//    public Map<String, Object> backTesting(String data){
//        HashMap<String, String> dt = new HashMap<>();
//        dt.put("action", "backtesting");
//        dt.put("args", data);
//        AjaxResult ajaxResult = new AjaxResult(0, "backTesting", dt);
//        return this.sendDataToPython(ajaxResult);
//    }

//    private Map<String, Object> addStrategy(){
//        return ;
//    }
}
