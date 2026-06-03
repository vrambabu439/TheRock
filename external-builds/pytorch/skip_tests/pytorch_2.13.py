# Copyright Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

skip_tests = {
    "common": {
        "nn": [
            # AssertionError: False is not true : Expected NaN in pdist output
            # AssertionError: Scalars are not close!
            # Expected 3.875156879425049 but got 3.876049757003784.
            # Absolute difference: 0.0008928775787353516 (up to 1e-05 allowed)
            # Relative difference: 0.0002304106921389532 (up to 1.3e-06 allowed)
            "test_CTCLoss_cudnn_cuda",
        ],
        "convolution": [
            # ROCm/MIOpen native hang in deterministic cuDNN Conv2d generated tests.
            # Covers dilation 1/2/3 across dtype variants; replaces file-level nn/test_convolution exclusion.
            "test_Conv2d_deterministic_cudnn",
        ],
        "distributions": [
            # SIGSEGV - OpenBLAS exceeds precompiled 128-thread hard limit
            # even with OPENBLAS_NUM_THREADS=64; crash in wishart.log_prob
            "test_entropy_monte_carlo",
        ],
        "dynamo": [
            # CI GPU isolation warning contaminates this exact stderr log assertion.
            "test_logs_out",
        ],
        "export": [
            # TestExportOnFakeCudaCUDA - subprocess import fails: missing librocm_sysdeps_liblzma.so.5
            "test_fake_export___getitem___cuda_float32",
            "test_fake_export_nn_functional_batch_norm_cuda_float32",
            "test_fake_export_nn_functional_batch_norm_without_cudnn_cuda_float32",
            "test_fake_export_nn_functional_conv2d_cuda_float32",
            "test_fake_export_nn_functional_instance_norm_cuda_float32",
            "test_fake_export_nn_functional_multi_margin_loss_cuda_float32",
            "test_fake_export_nn_functional_scaled_dot_product_attention_cuda_float32",
            "test_fake_export_nonzero_cuda_float32",
            "test_preserve_original_behavior_cuda",
        ],
        "inductor": [
            # TestOpInfoPropertiesCUDA - ROCm 7.13 eager vs Triton log/log10 bitwise drift
            "test_eager_equivalence_log10_backend_inductor_default_cuda_float32",
            "test_eager_equivalence_log_backend_inductor_default_cuda_float16",
            "test_eager_equivalence_log_backend_inductor_default_cuda_float32",
            "test_unary_ufunc_numerical_log10_backend_inductor_default_cuda_float16",
            "test_unary_ufunc_numerical_log10_backend_inductor_default_cuda_float32",
            "test_unary_ufunc_numerical_log_backend_inductor_default_cuda_bfloat16",
            "test_unary_ufunc_numerical_log_backend_inductor_default_cuda_float16",
            "test_unary_ufunc_numerical_log_backend_inductor_default_cuda_float32",
            # ExtensionBackendTests - extension_device registration/is_available handling
            "test_open_device_registration",
            # inductor/test_user_streams: stream/cudagraph structure mismatches and hangs on ROCm.
            "test_codegen_structure_parallel_matmuls",
            "test_codegen_structure_pipeline",
            "test_codegen_structure_single_stream",
            "test_explicit_current_stream_with_cudagraphs",
            "test_implicit_current_stream_with_cudagraphs",
            # inductor/test_autoheuristic: compute_cap is a string in ROCm wheel metadata.
            # pytest -k also matches the file name, so exclude neighboring tests explicitly.
            "(AutoHeuristicTest and not test_autoheuristic_a100 and not test_autoheuristic_h100 and not test_autoheuristic_pad_mm and not test_global_feedback and not test_mixed_mm_a100 and not test_pad_mm_autoheuristic_deterministic_mode)",
            # inductor/test_aot_inductor_package: AOTI C++ package tests need
            # more complete CMake/runtime library-path handling in the wheel CI lane.
            "test_compile_after_package_multi_arch",
            "test_compile_after_package_static",
            "test_compile_standalone_cos",
            "test_compile_with_exporter",
            "test_compile_with_exporter_weights",
        ],
        "fx": [
            # test_fx: backward-compatibility expectation drift.
            "test_function_back_compat",
        ],
        "schema_check": [
            # test_schema_check: multinomial bf16 schema check can hang GPU on ROCm.
            "test_schema_correctness_multinomial_cuda_bfloat16",
        ],
        "modules": [
            # TestModuleCUDA - CTCLoss cpu/gpu parity scalar mismatch
            "test_cpu_gpu_parity_nn_CTCLoss_cuda_float32",
            # TestModuleCUDA - CTCLoss forward scalar mismatch
            "test_forward_nn_CTCLoss_cuda_float32",
        ],
        "multiprocessing": [
            # ROCm devel/runtime-dependent UTs. Skip in the PyTorch full-suite
            # lane; these are expected to run in the separate ROCm devel UT step.
            "(test_fs and not test_fs_)",
            "test_fs_is_shared",
            "test_fs_pool",
            "test_fs_preserve_sharing",
            "test_fs_sharing",
        ],
        "serialization": [
            # TestSerialization - NJT weights_only import check
            # TestOldSerialization - CI env assertion
            "test_debug_set_in_ci",
        ],
        "utils": [
            # ROCm devel/runtime-dependent UT. Skip in the PyTorch full-suite lane;
            # this is expected to run in the separate ROCm devel UT step.
            "test_load_standalone",
        ],
        "distributed": [
            # DistMathOpsTest - torch.linalg.eig requires MAGMA in this build.
            "test_linalg_ops",

            # ROCm bump attribution anchors:
            # - Apr20/PT + Apr20/ROCm control was green across distributed
            #   shards: run 25244506667; jobs 74051598033 (1/3),
            #   74051597989 (2/3), 74051597951 (3/3).
            # - Apr20/PT + May01/ROCm first attribution failures:
            #   run 25925372276; jobs 76205215134 (1/3),
            #   76205215167 (2/3), 76205215147 (3/3).
            # - Apr20/PT + May01/ROCm second attribution failures:
            #   run 26136844778; jobs 76873873289 (1/3),
            #   76873873320 (2/3), 76873873274 (3/3).

            # Run 25925372276 shard 3/3, job 76205215147:
            # https://github.com/ROCm/TheRock/actions/runs/25925372276/job/76205215147
            # Mixed-precision cast crash bucket. Jun1 CI still hit bf16 SIGSEGVs.
            "(TestFullyShardMixedPrecisionCasts)",
            "(TestReplicateMixedPrecisionCasts and test_norm_modules_bf16)",

            # Originally added as part of the May01 mixed-precision attribution
            # layer. Not covered by the Jun1 validation runs; siblings in
            # TestFullyShardMixedPrecisionCasts above still SIGSEGV on bf16, so
            # keep these training-variant skips until a targeted validation run
            # against distributed/_composable/fsdp/test_fully_shard_training
            # proves them passing on Jun1/Jun1.
            "(TestFullyShardMixedPrecisionTraining and test_compute_dtype)",
            "(TestFullyShardMixedPrecisionTraining and test_grad_acc_with_reduce_dtype)",
            "(TestFullyShardMixedPrecisionTraining and test_reduce_dtype)",
            "(TestFullyShardMixedPrecisionTraining and test_structured_input_output)",

            # Run 25925372276 shard 2/3, job 76205215167:
            # https://github.com/ROCm/TheRock/actions/runs/25925372276/job/76205215167
            # Attribution-only DTensor/runtime checks not covered by the Jun1 run set.
            "(DistElementwiseOpsTest and test_dropout_errors)",

            # Run 26136844778 shard 2/3, job 76873873320: elastic launcher
            # ChildFailedError/SIGABRT bucket.
            "(ElasticLaunchTest and test_virtual_local_rank)",

            # CI run 26296106703 distributed shard 1/3, confirmed still failing in
            # Jun1 CI run 26858601551.
            "(ReplicateTest and test_compile_bf16)",

            # Run 26170912739 shard 2/3, job 76988162878:
            # https://github.com/ROCm/TheRock/actions/runs/26170912739/job/76988162878
            # fp16 was not definitively revalidated because the bf16 sibling still
            # SIGSEGVs before the module can complete.
            "(TestReplicateMixedPrecisionCasts and test_norm_modules_fp16)",

            # CI run 26794193808 distributed shards 2/3 and 3/3; confirmed still
            # failing in Jun1 CI run 26858374424.
            "(CommTest and test_profiler_nccl_annotations_on_gpu_kernels_use_python_export_True)",
            "(CommTest and test_profiler_nccl_annotations_on_gpu_kernels_use_python_export_False)",
        ],
    },
}
