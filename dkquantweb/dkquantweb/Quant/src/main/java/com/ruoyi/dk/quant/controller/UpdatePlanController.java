package com.ruoyi.dk.quant.controller;

import java.util.List;

import io.swagger.annotations.Api;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import com.ruoyi.dk.quant.constants.ApiResponse;
import com.ruoyi.dk.quant.domain.UpdatePlan;
import com.ruoyi.dk.quant.domain.UpdatePlanRecord;
import com.ruoyi.dk.quant.service.IUpdatePlanService;
import com.ruoyi.dk.quant.service.IUpdatePlanRecordService;

/**
 * 更新计划 控制层
 */
@Api(tags = "更新计划")
@RestController
@RequestMapping("/system/updatePlan")
public class UpdatePlanController {
    @Autowired
    private IUpdatePlanService updatePlanService;
    
    @Autowired
    private IUpdatePlanRecordService updatePlanRecordService;

    /**
     * 获取更新计划列表
     */

    @GetMapping("/list")
    public ApiResponse list(UpdatePlan updatePlan) {
        try {
            // 设置分页参数
            List<UpdatePlan> list = updatePlanService.selectUpdatePlanList(updatePlan);
            int count = updatePlanService.selectUpdatePlanCount(updatePlan);
            return ApiResponse.success("获取成功", list, count);
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("获取更新计划列表失败");
        }
    }

    /**
     * 获取更新计划详细信息
     */
    @GetMapping("/{id}")
    public ApiResponse getInfo(@PathVariable("id") Long id) {
        try {
            UpdatePlan updatePlan = updatePlanService.selectUpdatePlanById(id);
            if (updatePlan != null) {
                return ApiResponse.success("获取成功", updatePlan);
            } else {
                return ApiResponse.error("未找到相关更新计划");
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("获取更新计划详情失败");
        }
    }

    /**
     * 新增更新计划
     */
    @PreAuthorize("@ss.hasAnyRoles('admin')")
    @PostMapping
    public ApiResponse add(@RequestBody UpdatePlan updatePlan) {
        try {
            int rows = updatePlanService.insertUpdatePlan(updatePlan);
            if (rows > 0) {
                return ApiResponse.success("新增成功");
            } else {
                return ApiResponse.error("新增失败");
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("新增更新计划失败");
        }
    }

    /**
     * 修改更新计划
     */
    @PreAuthorize("@ss.hasAnyRoles('admin')")
    @PutMapping
    public ApiResponse edit(@RequestBody UpdatePlan updatePlan) {
        try {
            int rows = updatePlanService.updateUpdatePlan(updatePlan);
            if (rows > 0) {
                return ApiResponse.success("修改成功");
            } else {
                return ApiResponse.error("修改失败");
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("修改更新计划失败");
        }
    }

    /**
     * 删除更新计划
     */
    @PreAuthorize("@ss.hasAnyRoles('admin')")
    @DeleteMapping("/{ids}")
    public ApiResponse remove(@PathVariable Long[] ids) {
        try {
            int rows = updatePlanService.deleteUpdatePlanByIds(ids);
            if (rows > 0) {
                return ApiResponse.success("删除成功");
            } else {
                return ApiResponse.error("删除失败");
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("删除更新计划失败");
        }
    }
    
    /**
     * 获取更新计划记录列表
     */
    @GetMapping("/record/list")
    public ApiResponse recordList(UpdatePlanRecord updatePlanRecord) {
        try {
            List<UpdatePlanRecord> list = updatePlanRecordService.selectUpdatePlanRecordList(updatePlanRecord);
            return ApiResponse.success("获取成功", list);
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("获取更新计划记录列表失败");
        }
    }
    
    /**
     * 获取更新计划的所有记录
     */
    @GetMapping("/record/plan/{planId}")
    public ApiResponse getPlanRecords(@PathVariable("planId") Long planId) {
        try {
            List<UpdatePlanRecord> list = updatePlanRecordService.selectUpdatePlanRecordsByPlanId(planId);
            return ApiResponse.success("获取成功", list);
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("获取更新计划记录失败");
        }
    }
    
    /**
     * 新增更新记录
     */
    @PostMapping("/record")
    public ApiResponse addRecord(@RequestBody UpdatePlanRecord updatePlanRecord) {
        try {
            int rows = updatePlanRecordService.insertUpdatePlanRecord(updatePlanRecord);
            if (rows > 0) {
                return ApiResponse.success("新增成功");
            } else {
                return ApiResponse.error("新增失败");
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("新增更新记录失败");
        }
    }
    
    /**
     * 修改更新记录
     */
    @PreAuthorize("@ss.hasAnyRoles('admin')")
    @PutMapping("/record")
    public ApiResponse editRecord(@RequestBody UpdatePlanRecord updatePlanRecord) {
        try {
            int rows = updatePlanRecordService.updateUpdatePlanRecord(updatePlanRecord);
            if (rows > 0) {
                return ApiResponse.success("修改成功");
            } else {
                return ApiResponse.error("修改失败");
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("修改更新记录失败");
        }
    }
    
    /**
     * 删除更新记录
     */
    @PreAuthorize("@ss.hasAnyRoles('admin')")
    @DeleteMapping("/record/{ids}")
    public ApiResponse removeRecord(@PathVariable Long[] ids) {
        try {
            int rows = updatePlanRecordService.deleteUpdatePlanRecordByIds(ids);
            if (rows > 0) {
                return ApiResponse.success("删除成功");
            } else {
                return ApiResponse.error("删除失败");
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ApiResponse.error("删除更新记录失败");
        }
    }
} 