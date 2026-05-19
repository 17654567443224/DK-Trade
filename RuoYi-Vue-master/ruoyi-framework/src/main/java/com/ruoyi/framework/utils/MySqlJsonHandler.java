package com.ruoyi.framework.utils;

import com.fasterxml.jackson.core.type.TypeReference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.apache.ibatis.type.BaseTypeHandler;
import org.apache.ibatis.type.JdbcType;

import java.sql.CallableStatement;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class MySqlJsonHandler<T> extends BaseTypeHandler<T> {

    private static final Logger logger = LoggerFactory.getLogger(MySqlJsonHandler.class);
    private static final ObjectMapper mapper = new ObjectMapper();
    private final TypeReference<T> typeReference;

    /**
     * 构造函数，用于非泛型类型
     *
     * @param clazz 目标类型
     */
    public MySqlJsonHandler(Class<T> clazz) {
        if (clazz == null) throw new IllegalArgumentException("Type argument cannot be null");
        this.typeReference = new TypeReference<T>() {
            @Override
            public Class<T> getType() {
                return clazz;
            }
        };
    }

    /**
     * 构造函数，用于泛型类型
     *
     * @param typeReference 目标类型的 TypeReference
     */
    public MySqlJsonHandler(TypeReference<T> typeReference) {
        if (typeReference == null) throw new IllegalArgumentException("TypeReference argument cannot be null");
        this.typeReference = typeReference;
    }

    static {
        mapper.configure(SerializationFeature.WRITE_NULL_MAP_VALUES, false);
        mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
    }

    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, T parameter, JdbcType jdbcType) throws SQLException {
        ps.setString(i, this.toJson(parameter));
    }

    @Override
    public T getNullableResult(ResultSet rs, String columnName) throws SQLException {
        return this.toObject(rs.getString(columnName));
    }

    @Override
    public T getNullableResult(ResultSet rs, int columnIndex) throws SQLException {
        return this.toObject(rs.getString(columnIndex));
    }

    @Override
    public T getNullableResult(CallableStatement cs, int columnIndex) throws SQLException {
        return this.toObject(cs.getString(columnIndex));
    }

    /**
     * 将 JSON 字符串转换为对象
     *
     * @param content JSON 字符串
     * @return 目标类型的对象
     */
    private T toObject(String content) {
        if (content != null && !content.isEmpty()) {
            try {
                return mapper.readValue(content, typeReference);
            } catch (Exception e) {
                logger.error("Failed to convert JSON string to object: {}", content, e);
                throw new RuntimeException("Failed to convert JSON string to object", e);
            }
        } else {
            return null;
        }
    }

    /**
     * 将对象转换为 JSON 字符串
     *
     * @param object 要转换的对象
     * @return JSON 字符串
     */
    private String toJson(T object) {
        try {
            return mapper.writeValueAsString(object);
        } catch (Exception e) {
            logger.error("Failed to convert object to JSON string: {}", object, e);
            throw new RuntimeException("Failed to convert object to JSON string", e);
        }
    }
}
