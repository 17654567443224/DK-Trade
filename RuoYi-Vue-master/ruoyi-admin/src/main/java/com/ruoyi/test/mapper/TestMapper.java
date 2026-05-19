package com.ruoyi.test.mapper;

import java.util.List;
import com.ruoyi.test.domain.Test;

/**
 * 测试用Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-01
 */
public interface TestMapper 
{
    /**
     * 查询测试用
     * 
     * @param id 测试用主键
     * @return 测试用
     */
    public Test selectTestById(Long id);

    /**
     * 查询测试用列表
     * 
     * @param test 测试用
     * @return 测试用集合
     */
    public List<Test> selectTestList(Test test);

    /**
     * 新增测试用
     * 
     * @param test 测试用
     * @return 结果
     */
    public int insertTest(Test test);

    /**
     * 修改测试用
     * 
     * @param test 测试用
     * @return 结果
     */
    public int updateTest(Test test);

    /**
     * 删除测试用
     * 
     * @param id 测试用主键
     * @return 结果
     */
    public int deleteTestById(Long id);

    /**
     * 批量删除测试用
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteTestByIds(Long[] ids);
}
