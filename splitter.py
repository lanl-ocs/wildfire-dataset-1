import pyarrow.parquet as pq
import sys


def split_parquet_by_rowgroup(source_file, output_file1, output_file2):
    pf = pq.ParquetFile(source_file)

    # Check the number of row groups
    num_row_groups = pf.num_row_groups
    assert num_row_groups == 6, f"Expected 6 row groups, found {num_row_groups}"

    # Split indices
    first_half = list(range(0, 3))
    second_half = list(range(3, 6))

    def copy_row_groups(row_group_indices, output_path):
        writer = None
        for i in row_group_indices:
            row_group = pf.read_row_group(i)
            if writer is None:
                writer = pq.ParquetWriter(
                    output_path,
                    row_group.schema,
                    version=pf.metadata.format_version,
                    compression=None,
                    use_dictionary=False,
                )
            writer.write(row_group, row_group_size=row_group.num_rows)
        if writer:
            writer.close()

    copy_row_groups(first_half, output_file1)
    copy_row_groups(second_half, output_file2)


# ==Usage spliter.py input.parquet split1.parquet, split2.parquet
split_parquet_by_rowgroup(sys.argv[1], sys.argv[2], sys.argv[3])
