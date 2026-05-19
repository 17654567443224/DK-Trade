package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.TargetMethodsMapper;
import com.ruoyi.dk.quant.domain.TargetMethods;
import com.ruoyi.dk.quant.service.ITargetMethodsService;

/**
 * 指标Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@Service
public class TargetMethodsServiceImpl implements ITargetMethodsService 
{
    @Autowired
    private TargetMethodsMapper targetMethodsMapper;

    /**
     * 查询指标
     * 
     * @param id 指标主键
     * @return 指标
     */
    @Override
    public TargetMethods selectTargetMethodsById(Long id)
    {
        return targetMethodsMapper.selectTargetMethodsById(id);
    }

    /**
     * 查询指标列表
     * 
     * @param targetMethods 指标
     * @return 指标
     */
    @Override
    public List<TargetMethods> selectTargetMethodsList(TargetMethods targetMethods)
    {
        return targetMethodsMapper.selectTargetMethodsList(targetMethods);
    }

    /**
     * 新增指标
     * 
     * @param targetMethods 指标
     * @return 结果
     */
    @Override
    public int insertTargetMethods(TargetMethods targetMethods)
    {
        return targetMethodsMapper.insertTargetMethods(targetMethods);
    }

    /**
     * 修改指标
     * 
     * @param targetMethods 指标
     * @return 结果
     */
    @Override
    public int updateTargetMethods(TargetMethods targetMethods)
    {
        return targetMethodsMapper.updateTargetMethods(targetMethods);
    }

    /**
     * 批量删除指标
     * 
     * @param ids 需要删除的指标主键
     * @return 结果
     */
    @Override
    public int deleteTargetMethodsByIds(Long[] ids)
    {
        return targetMethodsMapper.deleteTargetMethodsByIds(ids);
    }

    /**
     * 删除指标信息
     * 
     * @param id 指标主键
     * @return 结果
     */
    @Override
    public int deleteTargetMethodsById(Long id)
    {
        return targetMethodsMapper.deleteTargetMethodsById(id);
    }
}
