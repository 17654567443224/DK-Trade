package com.ruoyi.test.service.impl;

import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.test.mapper.TestMapper;
import com.ruoyi.test.domain.Test;
import com.ruoyi.test.service.ITestService;

/**
 * 测试用Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-01
 */
@Service
public class TestServiceImpl implements ITestService 
{
    @Autowired
    private TestMapper testMapper;

    /**
     * 查询测试用
     * 
     * @param id 测试用主键
     * @return 测试用
     */
    @Override
    public Test selectTestById(Long id)
    {
        return testMapper.selectTestById(id);
    }

    /**
     * 查询测试用列表
     * 
     * @param test 测试用
     * @return 测试用
     */
    @Override
    public List<Test> selectTestList(Test test)
    {
        return testMapper.selectTestList(test);
    }

    /**
     * 新增测试用
     * 
     * @param test 测试用
     * @return 结果
     */
    @Override
    public int insertTest(Test test)
    {
        test.setCreateTime(DateUtils.getNowDate());
        return testMapper.insertTest(test);
    }

    /**
     * 修改测试用
     * 
     * @param test 测试用
     * @return 结果
     */
    @Override
    public int updateTest(Test test)
    {
        test.setUpdateTime(DateUtils.getNowDate());
        return testMapper.updateTest(test);
    }

    /**
     * 批量删除测试用
     * 
     * @param ids 需要删除的测试用主键
     * @return 结果
     */
    @Override
    public int deleteTestByIds(Long[] ids)
    {
        return testMapper.deleteTestByIds(ids);
    }

    /**
     * 删除测试用信息
     * 
     * @param id 测试用主键
     * @return 结果
     */
    @Override
    public int deleteTestById(Long id)
    {
        return testMapper.deleteTestById(id);
    }
}
