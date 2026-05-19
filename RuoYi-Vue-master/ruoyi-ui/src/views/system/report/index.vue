<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="余额" prop="finalBalance">
        <el-input
          v-model="queryParams.finalBalance"
          placeholder="请输入余额"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="最大回撤" prop="maxDrawdown">
        <el-input
          v-model="queryParams.maxDrawdown"
          placeholder="请输入最大回撤"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="胜率" prop="winRate">
        <el-input
          v-model="queryParams.winRate"
          placeholder="请输入胜率"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="最大盈利" prop="maxProfit">
        <el-input
          v-model="queryParams.maxProfit"
          placeholder="请输入最大盈利"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="最大亏损" prop="maxLoss">
        <el-input
          v-model="queryParams.maxLoss"
          placeholder="请输入最大亏损"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="交易总数" prop="totalTrades">
        <el-input
          v-model="queryParams.totalTrades"
          placeholder="请输入交易总数"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="夏普比率" prop="sharpeRatio">
        <el-input
          v-model="queryParams.sharpeRatio"
          placeholder="请输入夏普比率"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="年化" prop="annualizedReturn">
        <el-input
          v-model="queryParams.annualizedReturn"
          placeholder="请输入年化"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="总收益率" prop="totalPnlratio">
        <el-input
          v-model="queryParams.totalPnlratio"
          placeholder="请输入总收益率"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['system:report:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:report:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:report:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['system:report:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="reportList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="策略ID" align="center" prop="id" />
      <el-table-column label="余额" align="center" prop="finalBalance" />
      <el-table-column label="最大回撤" align="center" prop="maxDrawdown" />
      <el-table-column label="胜率" align="center" prop="winRate" />
      <el-table-column label="最大盈利" align="center" prop="maxProfit" />
      <el-table-column label="最大亏损" align="center" prop="maxLoss" />
      <el-table-column label="交易总数" align="center" prop="totalTrades" />
      <el-table-column label="夏普比率" align="center" prop="sharpeRatio" />
      <el-table-column label="年化" align="center" prop="annualizedReturn" />
      <el-table-column label="总收益率" align="center" prop="totalPnlratio" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['system:report:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['system:report:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改策略绩效指标对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="余额" prop="finalBalance">
          <el-input v-model="form.finalBalance" placeholder="请输入余额" />
        </el-form-item>
        <el-form-item label="最大回撤" prop="maxDrawdown">
          <el-input v-model="form.maxDrawdown" placeholder="请输入最大回撤" />
        </el-form-item>
        <el-form-item label="胜率" prop="winRate">
          <el-input v-model="form.winRate" placeholder="请输入胜率" />
        </el-form-item>
        <el-form-item label="最大盈利" prop="maxProfit">
          <el-input v-model="form.maxProfit" placeholder="请输入最大盈利" />
        </el-form-item>
        <el-form-item label="最大亏损" prop="maxLoss">
          <el-input v-model="form.maxLoss" placeholder="请输入最大亏损" />
        </el-form-item>
        <el-form-item label="交易总数" prop="totalTrades">
          <el-input v-model="form.totalTrades" placeholder="请输入交易总数" />
        </el-form-item>
        <el-form-item label="夏普比率" prop="sharpeRatio">
          <el-input v-model="form.sharpeRatio" placeholder="请输入夏普比率" />
        </el-form-item>
        <el-form-item label="年化" prop="annualizedReturn">
          <el-input v-model="form.annualizedReturn" placeholder="请输入年化" />
        </el-form-item>
        <el-form-item label="总收益率" prop="totalPnlratio">
          <el-input v-model="form.totalPnlratio" placeholder="请输入总收益率" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listReport, getReport, delReport, addReport, updateReport } from "@/api/system/report";

export default {
  name: "Report",
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 策略绩效指标表格数据
      reportList: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        finalBalance: null,
        maxDrawdown: null,
        winRate: null,
        maxProfit: null,
        maxLoss: null,
        totalTrades: null,
        sharpeRatio: null,
        annualizedReturn: null,
        totalPnlratio: null
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        finalBalance: [
          { required: true, message: "余额不能为空", trigger: "blur" }
        ],
        maxDrawdown: [
          { required: true, message: "最大回撤不能为空", trigger: "blur" }
        ],
        winRate: [
          { required: true, message: "胜率不能为空", trigger: "blur" }
        ],
        maxProfit: [
          { required: true, message: "最大盈利不能为空", trigger: "blur" }
        ],
        maxLoss: [
          { required: true, message: "最大亏损不能为空", trigger: "blur" }
        ],
        totalTrades: [
          { required: true, message: "交易总数不能为空", trigger: "blur" }
        ],
        sharpeRatio: [
          { required: true, message: "夏普比率不能为空", trigger: "blur" }
        ],
        annualizedReturn: [
          { required: true, message: "年化不能为空", trigger: "blur" }
        ],
        totalPnlratio: [
          { required: true, message: "总收益率不能为空", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询策略绩效指标列表 */
    getList() {
      this.loading = true;
      listReport(this.queryParams).then(response => {
        this.reportList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        id: null,
        finalBalance: null,
        maxDrawdown: null,
        winRate: null,
        maxProfit: null,
        maxLoss: null,
        totalTrades: null,
        sharpeRatio: null,
        annualizedReturn: null,
        totalPnlratio: null
      };
      this.resetForm("form");
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加策略绩效指标";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids
      getReport(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改策略绩效指标";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.id != null) {
            updateReport(this.form).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addReport(this.form).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const ids = row.id || this.ids;
      this.$modal.confirm('是否确认删除策略绩效指标编号为"' + ids + '"的数据项？').then(function() {
        return delReport(ids);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('system/report/export', {
        ...this.queryParams
      }, `report_${new Date().getTime()}.xlsx`)
    }
  }
};
</script>
