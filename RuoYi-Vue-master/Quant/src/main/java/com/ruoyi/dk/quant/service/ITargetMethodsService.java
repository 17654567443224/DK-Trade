package com.ruoyi.dk.quant.service;

import java.util.List;
import com.ruoyi.dk.quant.domain.TargetMethods;

/**
 * 指标Service接口
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public interface ITargetMethodsService 
{
    /**
     * 查询指标
     * 
     * @param id 指标主键
     * @return 指标
     */
    public TargetMethods selectTargetMethodsById(Long id);

    /**
     * 查询指标列表
     * 
     * @param targetMethods 指标
     * @return 指标集合
     */
    public List<TargetMethods> selectTargetMethodsList(TargetMethods targetMethods);

    /**
     * 新增指标
     * 
     * @param targetMethods 指标
     * @return 结果
     */
    public int insertTargetMethods(TargetMethods targetMethods);

    /**
     * 修改指标
     * 
     * @param targetMethods 指标
     * @return 结果
     */
    public int updateTargetMethods(TargetMethods targetMethods);

    /**
     * 批量删除指标
     * 
     * @param ids 需要删除的指标主键集合
     * @return 结果
     */
    public int deleteTargetMethodsByIds(Long[] ids);

    /**
     * 删除指标信息
     * 
     * @param id 指标主键
     * @return 结果
     */
    public int deleteTargetMethodsById(Long id);
}
